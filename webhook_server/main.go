package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
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
	Html_url  string       `json:"html_url"`
	Owner     github_owner `json:"owner"`
}

type github_sender struct {
	Url        string `json:"url"`
	Login      string `json:"login"`
	Id         int    `json:"id"`
	Avatar_url string `json:"avatar_url"`
}

type github_head_commit struct {
	Url      string   `json:"url"`
	Message  string   `json:"message"`
	Added    []string `json:"added"`
	Removed  []string `json:"removed"`
	Modified []string `json:"modified"`
}

type github_commits struct {
	Id string `json:"id"`
}

type github_webhook struct {
	Id          string
	Action      string             `json:"action"`
	Issue       github_issue       `json:"issue"`
	Repository  github_repository  `json:"repository"`
	Sender      github_sender      `json:"sender"`
	Private     bool               `json:"private"`
	Full_name   string             `json:"full_name"`
	Head_commit github_head_commit `json:"head_commit"`
}

type Response struct {
	Id            string
	Event         string `json:"message"`
	Rep_name      string `json:"rep_name"`
	Rep_link      string `json:"rep_link"`
	Author        string `json:"author"`
	Author_url    string `json:"author_url"`
	Author_avatar string `json:"avatar_url"`
	Comment       string `json:"comment"`
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
	dispatcher.RegisterHandler("push", commit)
	fmt.Printf("%+v\n", dispatcher)
	return dispatcher
}

func commit(payload *github_webhook) error {

	event := "Сделан коммит"
	repository_name := payload.Repository.Full_name
	rep_link := payload.Repository.Html_url
	author_name := payload.Sender.Login
	author_url := payload.Sender.Url
	avatar_url := payload.Sender.Avatar_url
	comment := payload.Head_commit.Message

	rep := Response{
		Id:            payload.Id,
		Event:         event,
		Author:        author_name,
		Author_url:    author_url,
		Author_avatar: avatar_url,
		Rep_name:      repository_name,
		Rep_link:      rep_link,
		Comment:       comment,
	}

	jsonData, err := json.Marshal(rep)
	if err != nil {
		return err
	}
	resp, err := http.Post(
		"http://127.0.0.1:5000/",
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		fmt.Println("Ошибка при отправке запроса:", err)
		return err
	}
	defer resp.Body.Close()
	return err
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
	webhookUrl := r.PathValue("webhookUrl")
	hook := github_webhook{}
	hook.Id = webhookUrl
	action := r.Header.Get("X-GitHub-Event")
	if action == "" {
		http.Error(w, "Missing X-GitHub-Event header", http.StatusBadRequest)
		return
	}
	fmt.Println(action)

	err := json.NewDecoder(r.Body).Decode(&hook)
	if err != nil {
		http.Error(w, fmt.Sprintf("Error decoding JSON: %v", err), http.StatusBadRequest)
		return
	}
	defer r.Body.Close()
	if err := dispatcher.Handle(action, &hook); err != nil {
		fmt.Printf("Error: %v\n", err)
	}

	return
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("POST /github-webhook/{webhookUrl}", handleWebhook)
	log.Fatal(http.ListenAndServe(":8080", mux))
}
