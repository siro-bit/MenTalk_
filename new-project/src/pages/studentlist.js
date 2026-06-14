import React, { useState, useEffect } from "react";
import StudenTable from "../components/studentable.js";
import "./studentlist.css";

function StudentList() {
    const [students, setStudents] = useState([]);
    const [search, setSearch] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [mentorNum, setMentorNum] = useState("");
    const [menteeNum, setMenteeNum] = useState("");

    const fetchStudents = async () => {
        try {
            setError(""); // 이전 에러 초기화
            setSuccess(""); // 이전 성공 메시지 초기화
            const response = await fetch("http://192.168.0.173:8000/get_student_info");

            if (!response.ok) {
                throw new Error(`서버 오류: ${response.status}`);
            }

            const data = await response.json();
            setStudents(data);
            setSuccess("학생 정보가 성공적으로 로드되었습니다.");
            console.log("학생 정보 로드 성공:", data);
        } catch (err) {
            console.error("학생 정보 로드 실패:", err);
            setError("학생 정보를 불러오는 데 실패했습니다. 다시 시도해주세요.");
            setSuccess(""); // 성공 메시지 초기화
        }
    };

    const addMentorMenteeMatch = async () => {
        try {
            setError("");
            setSuccess("");

            const response = await fetch(
                `http://192.168.0.173:8000/matching/${mentorNum}/${menteeNum}`,
                {
                    method: "PATCH"
                }
            );

            if (!response.ok) {
                throw new Error(`서버 오류: ${response.status}`);
            }

            const data = await response.json();

            //setStudents(data);
            setSuccess("멘토-멘티가 성공적으로 매칭되었습니다.");

            setMentorNum("");
            setMenteeNum("");

        } catch (err) {
            console.error(err);
            setError("멘토-멘티를 매칭하는 데 실패했습니다.");
        }
    };

    const handleMentorUpdate = (studentId, newIsMentor) => {
        setStudents(prevStudents =>
            prevStudents.map(student =>
                student.student_id === studentId
                    ? { ...student, is_mentor: newIsMentor }
                    : student
            )
        );
    };
    useEffect(() => {
        fetchStudents();
    }, []);

    const filteredStudents = students.filter(student =>
        student.name.includes(search) ||
        student.student_num.toString().includes(search)
    );


    return (

        <div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '10px' }}>
                <h2 style={{ alignItems: 'center', marginBottom: '5px' }}>학생 목록</h2>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                {success && <p style={{ color: 'green' }}>{success}</p>}
                <div style={{ display: 'flex', flexDirection: 'row', gap: '10px', alignItems: 'center', marginBottom: '10px' }}>
                    <input
                        type="text"
                        placeholder="학생 이름을 입력하세요"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        style={{ width: '200px', padding: '5px' }} />
                    <button onClick={fetchStudents} style={{ padding: '5px 10px' }}>
                        업데이트
                    </button>
                </div>
            </div>

            {/* 학생 등록 ui */}
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '10px' }}>
                <h3>멘토-멘티 매칭</h3>
                <input
                    value={mentorNum}
                    onChange={(e) => setMentorNum(e.target.value)}
                    type="text"
                    placeholder="멘토 번호"
                    style={{ width: '200px', padding: '5px', marginBottom: '5px' }}
                />
                <input
                    value={menteeNum}
                    onChange={(e) => setMenteeNum(e.target.value)}
                    type="text"
                    placeholder="멘티 번호"
                    style={{ width: '200px', padding: '5px', marginBottom: '5px' }}
                />
                <button onClick={addMentorMenteeMatch} style={{ padding: '5px 10px' }}>
                    매칭
                </button>
            </div>

            <StudenTable
                students={filteredStudents}
                onUpdateMentor={handleMentorUpdate}
                onMentorUpdateSuccess={fetchStudents}
            />
        </div>
    );
}

export default StudentList;