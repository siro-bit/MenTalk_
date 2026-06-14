import React from "react";
import { useNavigate } from "react-router-dom";

function StudenTable({students, onUpdateMentor, onMentorUpdateSuccess}) {
  const navigate = useNavigate(); // 페이지 이동 기능 사용

  // 학생 이름 클릭하면 신고 조회 페이지로 이동
  const goReportPage = (student) => {
    if (!student.reports || student.reports.length === 0) return; // 신고 없으면 이동 안함

    navigate("/report", {
      state: { student } // 신고 정보 전달
    });
  };

  const goChatPage = (student) => {
    if (!student.chat_room_id) return; // 채팅 룸 없으면 이동 안함

    navigate("/chat", {
      state: { numbers: [student.student_id, student.chat_room_id] } // 채팅 정보 전달
    });
  };

  const handleMentorUpdate = async (student) => {
    const newIsMentor = student.is_mentor === 0 ? 1 : 0;
    
    try {
      const response = await fetch(`http://192.168.0.173:8000/update_is_mentor/${student.student_id}/${newIsMentor}`, {
        method: "GET",
      });
      
      if (!response.ok) {
        throw new Error(`서버 오류: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("멘토 권한 업데이트 응답:", data); // 응답 데이터 확인
      
     
      if (response.ok && (data.success !== false)) {
        
        onUpdateMentor(student.student_id, newIsMentor);
        if (onMentorUpdateSuccess) {
          onMentorUpdateSuccess();
        }
        
      } else {
        alert("멘토 권한 업데이트 실패: " + (data.message || "알 수 없는 오류"));
      }
    } catch (error) {
      console.error("멘토 권한 업데이트 실패:", error);
      alert("멘토 권한 업데이트 중 오류가 발생했습니다. 다시 시도해주세요.");
    }
  };

  

  return (
    <table>
      <thead>
        <tr>
          <th>id</th>
          <th>이름</th>
          <th>학번</th>
          <th>멘토</th>
          <th>멘티</th>
          <th>멘토 권한</th>
          <th>채팅 룸 id</th>
          <th>이메일</th>         
        </tr>
      </thead>

      <tbody>
        {students.map(student => (
          <tr key={student.student_id}>
            <td style={{width:"5%"}}>{student.student_id}</td>
            <td>
              <span
                style={{
                  color: student.reports?.length > 0 ? "red" : "black", // 신고 있으면 빨간색
                  cursor: student.reports?.length > 0 ? "pointer" : "default" // 클릭 가능 표시
                }}
                onClick={() => goReportPage(student)} // 클릭하면 신고 페이지 이동
              >
                {student.name}
              </span>
            </td>
            <td>{student.student_num}</td>
            <td>{student.mentor_student_id == null ? "X" : student.mentor_student_id}</td>
            <td>{student.mentee_student_id == null ? "X" : student.mentee_student_id}</td>
            <td>
              {student.is_mentor == 0 ? "X" : "O"}
              <button style={{marginLeft: "10px"}} onClick={() => handleMentorUpdate(student)}>
                {student.is_mentor == 0 ? "멘토로 변경" : "멘토 해제"}
              </button>
            </td>
            <td>
              <span
                style={{
                  color: student.chat_room_id == 0 ? "red" : "black", // 채팅 룸이 없으면 주황색
                  cursor: student.chat_room_id == 0 ? "default" : "pointer" // 클릭 가능 표시
                }}
                onClick={() => goChatPage(student)} // 클릭하면 신고 페이지 이동
              >
              {student.chat_room_id == 0 ? "X" : student.chat_room_id}
              </span>
            </td>
            <td>
              {student.email || "X"}
            </td>    
            
          </tr>
        ))}
      </tbody>

    </table>
  );
}

export default StudenTable;
