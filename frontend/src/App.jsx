import { useState, useRef, useEffect } from "react";
import "./App.css";
import api from "./services/api";
import ReactMarkdown from "react-markdown";

function App() {
  const [repository, setRepository] = useState("");
  const [question, setQuestion] = useState("");
  const [scannedRepo, setScannedRepo] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [isAsking, setIsAsking] = useState(false);
  const [isCheckingStatus, setIsCheckingStatus] = useState(true);

  const [messages, setMessages] = useState([
    {
      sender: "assistant",
      text: "Welcome to CodeSage AI. Scan a repository to begin.",
    },
  ]);

  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, isAsking]);

  useEffect(() => {
    const loadStatus = async () => {
      try {
        const response = await api.get("/status");

        if (response.data.repository_loaded) {
          setRepository(response.data.repository_url);
          setScannedRepo(response.data.repository_url);

          setMessages([
            {
              sender: "assistant",
              text: `Picking up where we left off. Ask me anything about **${response.data.repository_url}**.`,
            },
          ]);
        }
      } catch (error) {
        console.error(error);
      } finally {
        setIsCheckingStatus(false);
      }
    };

    loadStatus();
  }, []);

  const handleScan = async () => {
    if (!repository.trim() || isScanning) return;

    setIsScanning(true);

    try {
      const response = await api.post("/scan", {
        repository: repository,
      });

      if (response.data.error) {
        setMessages([
          {
            sender: "assistant",
            text: response.data.error,
          },
        ]);
        return;
      }

      setScannedRepo(repository.trim());

      setMessages([
        {
          sender: "assistant",
          text: response.data.already_scanned
            ? `Repository already analyzed. Ask me anything about **${repository.trim()}**.`
            : `Repository scanned successfully. Ask me anything about **${repository.trim()}**.`,
        },
      ]);
    } catch (error) {
      setMessages([
        {
          sender: "assistant",
          text: "Failed to scan repository. Check the URL and try again.",
        },
      ]);

      console.error(error);
    } finally {
      setIsScanning(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim() || isAsking) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setIsAsking(true);

    try {
      const response = await api.post("/ask", {
        question: userQuestion,
      });

      const text = response.data.answer ?? response.data.error;

      setMessages((prev) => [
        ...prev,
        {
          sender: "assistant",
          text: text,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "assistant",
          text: "Failed to get a response from the backend.",
        },
      ]);

      console.error(error);
    } finally {
      setIsAsking(false);
    }
  };

  const handleScanKeyDown = (e) => {
    if (e.key === "Enter") handleScan();
  };

  const handleAskKeyDown = (e) => {
    if (e.key === "Enter") handleAsk();
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>CodeSage AI</h1>
        <p className="tagline">
          {isCheckingStatus
            ? "// checking for a previous session"
            : scannedRepo
            ? `// reading — ${scannedRepo}`
            : "// repository intelligence, read closely"}
        </p>
      </header>

      <div className="scan-container">
        <input
          type="text"
          placeholder="GitHub repository URL"
          value={repository}
          onChange={(e) => setRepository(e.target.value)}
          onKeyDown={handleScanKeyDown}
          disabled={isScanning || isCheckingStatus}
        />

        <button
          className="scan-btn"
          onClick={handleScan}
          disabled={isScanning || isCheckingStatus}
        >
          {isScanning ? "Analyzing…" : "Scan"}
        </button>
      </div>

      {isScanning && (
        <div className="status status-scan">
          <p>
            Analyzing repository — parsing files, generating embeddings, building the search index.
          </p>
          <span className="status-bar" />
        </div>
      )}

      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((message, index) => (
          <div
            key={index}
            className={message.sender === "user" ? "message user" : "message assistant"}
          >
            {message.sender === "assistant" && <span className="gloss-label">codesage</span>}
            <ReactMarkdown>{message.text}</ReactMarkdown>
          </div>
        ))}
      </div>

      <div className="ask-container">
        <input
          type="text"
          placeholder="Ask about the repository…"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleAskKeyDown}
          disabled={isAsking}
        />

        <button className="ask-btn" onClick={handleAsk} disabled={isAsking}>
          {isAsking ? "Thinking…" : "Send"}
        </button>
      </div>

      {isAsking && (
        <div className="status status-ask">
          <p>Retrieving relevant code and generating an answer.</p>
          <span className="status-bar status-bar-sage" />
        </div>
      )}
    </div>
  );
}

export default App;