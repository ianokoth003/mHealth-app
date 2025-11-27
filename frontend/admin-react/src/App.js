import React from "react";
import Dashboard from "./pages/Dashboard";
import PatientPage from "./pages/PatientPage.jsx";
import "./testApi";


export default function App(){
  return (
    <div className="admin-root">
      <header className="admin-header"><h1>HealthEase Admin</h1></header>
      <main style={{padding:20}}>
        <Dashboard />
        <hr/>
        <PatientPage />
      </main>
    </div>
  );
}


