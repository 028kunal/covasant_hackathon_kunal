import React, { useEffect, useState, useCallback } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

const FormChat = () => {
    const [sessionId, setSessionId] = useState('kunal_session');
    const [fileName, setFileName] = useState('');
    const [question, setQuestion] = useState('');
    const [isListening, setIsListening] = useState(false);
    const [completed, setCompleted] = useState(false);
    const [started, setStarted] = useState(false);
    const { transcript, resetTranscript, listening } = useSpeechRecognition();

    const speak = (text) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-IN';
        window.speechSynthesis.speak(utterance);
    };

    const fetchNextQuestion = useCallback(async () => {
        try {
            const res = await fetch(`http://127.0.0.1:8000/chat/start?file_name=${fileName}&session_id=${sessionId}`, {
                method: 'POST'
            });
            const data = await res.json();
            if (data.question) {
                setQuestion(data.question);
                speak(data.question);
                setStarted(true);
            }
        } catch (error) {
            console.error(error);
            alert("Error fetching question. Check backend or file name.");
        }
    }, [fileName, sessionId]);

    const sendAnswer = useCallback(async (answerText) => {
        try {
            const res = await fetch(`http://127.0.0.1:8000/chat/answer?file_name=${fileName}&session_id=${sessionId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answer: answerText })
            });
            const data = await res.json();
            if (data.message.includes('completed')) {
                setCompleted(true);
                speak("Form filling completed. Thank you!");
            } else if (data.question) {
                setQuestion(data.question);
                speak(data.question);
            }
        } catch (error) {
            console.error(error);
            alert("Error sending answer. Check backend.");
        }
    }, [fileName, sessionId]);

    const handleStartListening = () => {
        resetTranscript();
        SpeechRecognition.startListening({ continuous: false, language: 'en-IN' });
        setIsListening(true);
    };

    const handleStopListening = useCallback(() => {
        SpeechRecognition.stopListening();
        setIsListening(false);
        if (transcript.trim()) {
            sendAnswer(transcript.trim());
            resetTranscript();
        }
    }, [transcript, sendAnswer, resetTranscript]);

    // Automatically stop listening when the user finishes speaking
    useEffect(() => {
        if (!listening && isListening) {
            handleStopListening();
        }
    }, [listening, isListening, handleStopListening]);

    if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
        return <span>Browser does not support Speech Recognition.</span>;
    }

    return (
        <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
            <h2>🗣️ Voice-Based Form Filler</h2>
            {!started ? (
                <>
                    <input
                        type="text"
                        placeholder="Enter file name (e.g., chat_flow_*.json)"
                        value={fileName}
                        onChange={(e) => setFileName(e.target.value)}
                        style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
                    />
                    <input
                        type="text"
                        placeholder="Enter session ID"
                        value={sessionId}
                        onChange={(e) => setSessionId(e.target.value)}
                        style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
                    />
                    <button onClick={fetchNextQuestion} style={{ padding: '10px 20px' }}>
                        Start Voice Form Fill
                    </button>
                </>
            ) : !completed ? (
                <>
                    <h3>Question:</h3>
                    <p>{question}</p>
                    <button onClick={isListening ? handleStopListening : handleStartListening} style={{ padding: '10px 20px' }}>
                        {isListening ? '🛑 Stop Recording' : '🎤 Answer via Voice'}
                    </button>
                    <p><strong>Transcript:</strong> {transcript}</p>
                    <p><strong>Status:</strong> {listening ? "Listening..." : "Idle"}</p>
                </>
            ) : (
                <h3>✅ Form filling completed successfully! Responses saved in backend folder.</h3>
            )}
        </div>
    );
};

export default FormChat;
