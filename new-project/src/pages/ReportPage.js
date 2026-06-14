import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function ReportPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const student = location.state?.student;
  const [message, setMessage] = useState("");
  const reports = student?.reports ? student.reports.split(',').filter(r => r.trim()) : [];
  
  if (!student) {
    return <div>신고 데이터가 없습니다.</div>;
  }

  const handleDeleteReport = async () => {
    try {
      const response = await fetch(`http://192.168.0.173:8000/delete_report/${student.student_id}`, {
        method: "GET"
      });

      if (!response.ok) {
        throw new Error(`서버 오류: ${response.status}`);
      }
      const data = await response.json();
      if (data.success === false) {
        setMessage(`삭제 실패: ${data.message || "알 수 없는 오류"}`);
        return;
      }
      setMessage("신고 내역이 삭제되었습니다.");
      setTimeout(() => {
        navigate(-1);
      }, 500);
    } catch (error) {
      console.error("신고 삭제 실패:", error);
      setMessage("신고 삭제 중 오류가 발생했습니다. 다시 시도해주세요.");
    }
  };

  return (
    <div>
      <h1>신고 조회 페이지</h1>
      <h2>학생 정보: {student.student_num} {student.name}</h2>
      <h3>신고 내역:</h3>
      <ul>
        {reports.map((report, index) => (
          <li key={index}>{report.trim()}</li>
        ))}
      </ul>
      <button onClick={handleDeleteReport} style={{ marginTop: "10px" }}>
        신고 내역 삭제
      </button>
      {message && <p style={{ color: "blue" }}>{message}</p>}
    </div>
  );
}

