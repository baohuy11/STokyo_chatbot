// import avatar from "../assets/avatar.jpg";
import robot_img from "../assets/robot_img";
import { useState, useRef, useEffect } from "react";
import ScaleLoader from "react-spinners/ScaleLoader";
import { TypeAnimation } from "react-type-animation";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMessage } from "@fortawesome/free-regular-sgv-icons";

function ChatBot(props) {
    const messagesEndRef = useRef(null);
    const [timeOfRequest, SetTimeOfRequest] = useState(0);
    let [promptInput, SetPromptInput] = useState("");
    let [sourceData, SetSourceData] = useState("stokyo");
    let [chatHistoty, SetChatHistory] = useState([]);

    const commonQuestions = [
        "奨学金を貰える条件",
        "",
        "",
    ]
}