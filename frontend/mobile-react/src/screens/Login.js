import React, {useState} from "react";
import api from "../api/axios";

export default function Login({onLogin}){
  const [email,setEmail]=useState("");
  const [password,setPassword]=useState("");
  const [err,setErr]=useState("");

  const submit = async (e)=>{
    e.preventDefault();
    try {
      const r = await api.post("/auth/login", { email, password });
      const token = r.data.access_token;
      onLogin(token);
      api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } catch (err) {
      setErr(err?.response?.data?.error || "Login failed");
    }
  };

  return (
    <div className="center">
      <h2>HealthEase — Worker Login</h2>
      <form onSubmit={submit}>
        <input placeholder="email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button>Login</button>
        {err && <div className="err">{err}</div>}
      </form>
    </div>
  );
}
