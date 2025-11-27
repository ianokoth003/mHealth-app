import React from "react";
import PatientList from "./PatientList";
import PatientForm from "./PatientForm";
import SyncScreen from "./SyncScreen";

export default function Home({token, unsyncedCount}){
  return (
    <div style={{padding:20}}>
      <header style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
        <h1>HealthEase - Mobile</h1>
        <div>Unsynced: {unsyncedCount}</div>
      </header>

      <section style={{display:"grid",gridTemplateColumns:"1fr 1fr", gap:20, marginTop:20}}>
        <div style={{background:"#fff",padding:12,borderRadius:8, boxShadow:"0 2px 6px rgba(0,0,0,.08)"}}>
          <h3>Register Patient</h3>
          <PatientForm />
        </div>
        <div style={{background:"#fff",padding:12,borderRadius:8, boxShadow:"0 2px 6px rgba(0,0,0,.08)"}}>
          <h3>Patients</h3>
          <PatientList />
        </div>
      </section>

      <div style={{marginTop:24}}>
        <SyncScreen />
      </div>
    </div>
  );
}
