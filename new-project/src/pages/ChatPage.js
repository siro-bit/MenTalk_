import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function ChatPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const numbers = location.state?.numbers;
  const [chat, setChat] = useState([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [st1, setStudent1Info] = useState("");
  const [st2, setStudent2Info] = useState("");
  
  const fetchChat = async () => {
      try {
          setError(""); // 이전 에러 초기화
          setSuccess(""); // 이전 성공 메시지 초기화
          const response = await fetch(`http://192.168.0.173:8000/get_chat/${numbers[0]}/${numbers[1]}`);
          
          if (!response.ok) {
              throw new Error(`서버 오류: ${response.status}`);
          }
          
          const data = await response.json();
          setChat(data);
          setSuccess("채팅 정보가 성공적으로 로드되었습니다.");
          console.log("채팅 정보 로드 성공:", data);
      } catch (err) {
          console.error("채팅 정보 로드 실패:", err);
          setError("채팅 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.");
          setSuccess(""); // 성공 메시지 초기화
      }
  };
    const fetchStudent1Info = async () => {
      try {
          setError(""); // 이전 에러 초기화
          setSuccess(""); // 이전 성공 메시지 초기화
          const response = await fetch(`http://192.168.0.173:8000/student_info/${numbers[0]}`);
          
          if (!response.ok) {
              throw new Error(`서버 오류: ${response.status}`);
          }
          
          const data = await response.json();
          setStudent1Info(data);
          setSuccess("학생 정보가 성공적으로 로드되었습니다.");
          console.log("학생 정보 로드 성공:", data);
      } catch (err) {
          console.error("학생 정보 로드 실패:", err);
          setError("학생 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.");
          setSuccess(""); // 성공 메시지 초기화
      }
    };
    const fetchStudent2Info = async () => {
      try {
          setError(""); // 이전 에러 초기화
          setSuccess(""); // 이전 성공 메시지 초기화
          const response = await fetch(`http://192.168.0.173:8000/student_info/${numbers[1]}`);
          
          if (!response.ok) {
              throw new Error(`서버 오류: ${response.status}`);
          }
          
          const data = await response.json();
          setStudent2Info(data);
          setSuccess("학생 정보가 성공적으로 로드되었습니다.");
          console.log("학생 정보 로드 성공:", data);
      } catch (err) {
          console.error("학생 정보 로드 실패:", err);
          setError("학생 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.");
          setSuccess(""); // 성공 메시지 초기화
      }
    };
  
  useEffect(() => {
        fetchChat();
        fetchStudent1Info();
        fetchStudent2Info();
      }, []);

  return (
    <div>
      <h1>채팅 조회 페이지</h1>
      <h3>채팅 내역</h3>
      {chat.map((ch) => (
          <li>{ch.sender_id == numbers[0] ? st1.name : st2.name} : {ch.message}</li> 
        ))}

    </div>
  );
}




