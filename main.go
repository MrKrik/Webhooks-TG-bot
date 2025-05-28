package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type github_issue struct {
	Url    string `json:"url"`
	Number int    `json:"number"`
}
type github_owner struct {
	Login string `json:"login"`
	Id    int    `json:"id"`
}

type github_repository struct {
	Id        int          `json:"id"`
	Full_name string       `json:"full_name"`
	Owner     github_owner `json:"owner"`
}

type github_sender struct {
	Login string `json:"login"`
	Id    int    `json:"id"`
}

type github_webhook struct {
	Action     string            `json:"action"`
	Issue      github_issue      `json:"issue"`
	Repository github_repository `json:"repository"`
	Sender     github_sender     `json:"sender"`
}

type WebhookDispatcher struct {
	handlers map[string]func(payload *github_webhook) error
}

func NewWebhookDispatcher() *WebhookDispatcher {
	return &WebhookDispatcher{
		handlers: make(map[string]func(payload *github_webhook) error),
	}
}

func (d *WebhookDispatcher) RegisterHandler(action string, handler func(payload *github_webhook) error) {
	d.handlers[action] = handler
}

func (d *WebhookDispatcher) Handle(action string, payload *github_webhook) error {
	if handler, exists := d.handlers[action]; exists {
		return handler(payload)
	}
	return fmt.Errorf("no handler found for action: %s", action)
}

func setupHandlers() *WebhookDispatcher {
	dispatcher := NewWebhookDispatcher()

	dispatcher.RegisterHandler("opened", opened)
	fmt.Printf("%+v\n", dispatcher)
	return dispatcher
}

func commit(payload *github_webhook) error {
	message := "Сделан коммит"
	commitAuthor := payload.Sender.Login
	repository_name := payload.Repository.Full_name
	issue_url := payload.Repository
}

func opened(payload *github_webhook) error {
	message := "Открыт вопрос"
	repository_name := payload.Repository.Full_name
	issue_url := payload.Issue.Url
	fmt.Println(message, repository_name, issue_url)
	return fmt.Errorf("f")
}

var dispatcher = setupHandlers()

func handleWebhook(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	contentType := r.Header.Get("Content-Type")
	if contentType != "application/json" {
		http.Error(w, "Content-Type must be application/json", http.StatusUnsupportedMediaType)
		return
	}

	hook := github_webhook{}

	err := json.NewDecoder(r.Body).Decode(&hook)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error decoding JSON: %v", err), http.StatusBadRequest)
		return
	}

	defer r.Body.Close()

	if err := dispatcher.Handle(hook.Action, &hook); err != nil {
		fmt.Printf("Error: %v\n", err)
	}

	return
}

func main() {

	client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI(" mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.6"))
	if err != nil {
		log.Fatal(err)
	}

	// Create connect
	err = client.Connect(context.TODO())
	if err != nil {
		log.Fatal(err)
	}

	// Check the connection
	err = client.Ping(context.TODO(), nil)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Connected to MongoDB!")

	mux := http.NewServeMux()
	mux.HandleFunc("POST /github-webhook/{webhookUrl}", handleWebhook)
	log.Fatal(http.ListenAndServe(":8080", mux))
}
