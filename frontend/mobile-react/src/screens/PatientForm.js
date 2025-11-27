import React, {useState} from "react";
import api from "../api/axios";
import { saveLocalRecord } from "../api/syncService";

export default function PatientForm(){
  const [first,setFirst]=useState("");
  const [last,setLast]=useState("");
  const [contact,setContact]=useState("");
  const [msg,setMsg]=useState("");
  const [errors,setErrors]=useState({});

  const validate = ()=>{
    const e = {};
    if (!first || first.trim().length===0) e.first = 'First name is required';
    if (!last || last.trim().length===0) e.last = 'Last name is required';
    return e;
  };

  const showMsg = (m)=>{ setMsg(m); setTimeout(()=>setMsg(''),3000); };

  const submit = async (e)=>{
    e.preventDefault();
    const eobj = validate();
    setErrors(eobj);
    if (Object.keys(eobj).length) {
      showMsg('Please fix validation errors');
      return;
    }

    const payload = {
      first_name:first,
      last_name:last,
      contact
    };
    // attempt to POST to server. If fails -> save locally
    try {
      await api.post("/patients/", payload);
      showMsg("Saved online");
      setFirst(""); setLast(""); setContact("");
    } catch (err) {
      await saveLocalRecord("patient", payload);
      showMsg("Saved locally (offline) — will sync when online");
      setFirst(""); setLast(""); setContact("");
    }
  };

  return (
    <form onSubmit={submit} style={{display:'flex',flexDirection:'column',gap:8}}>
      <div>
        <input placeholder="First name" value={first} onChange={e=>setFirst(e.target.value)} />
        {errors.first && <div style={{color:'red',fontSize:12}}>{errors.first}</div>}
      </div>
      <div>
        <input placeholder="Last name" value={last} onChange={e=>setLast(e.target.value)} />
        {errors.last && <div style={{color:'red',fontSize:12}}>{errors.last}</div>}
      </div>
      <div>
        <input placeholder="Contact" value={contact} onChange={e=>setContact(e.target.value)} />
      </div>
      <div>
        <button type="submit">Save Patient</button>
      </div>
      {msg && <div style={{position:'fixed',right:20,bottom:20,background:'#222',color:'#fff',padding:'8px 12px',borderRadius:6}}>{msg}</div>}
    </form>
  );
}
