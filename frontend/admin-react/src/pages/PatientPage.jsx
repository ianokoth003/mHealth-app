import React, {useState, useEffect} from "react";
import api from "../api/axios";

export default function PatientsPage(){
  const [items,setItems] = useState([]);
  const [qStr,setQStr] = useState("");
  const [page,setPage] = useState(1);
  const [perPage,setPerPage] = useState(10);
  const [total,setTotal] = useState(0);
  const [totalPages,setTotalPages] = useState(1);
  const [first,setFirst] = useState("");
  const [last,setLast] = useState("");
  const [contact,setContact] = useState("");
  const [dob,setDob] = useState("");
  const [sex,setSex] = useState("");
  const [address,setAddress] = useState("");
  const [clinicalId,setClinicalId] = useState("");
  const [allergies,setAllergies] = useState("");
  const [history,setHistory] = useState("");
  const [msg,setMsg] = useState("");
  const [selected,setSelected] = useState(null);
  const [error,setError] = useState("");
  const [polling,setPolling] = useState(null);

  useEffect(() => {
    fetchList();
    // start polling every 10 seconds
    const id = setInterval(()=>fetchList(), 10000);
    setPolling(id);
    return ()=>{ if (id) clearInterval(id); };
  }, []);

  const fetchList = async (p = page) =>{
    try {
      const r = await api.get("/patients", { params: { q: qStr || undefined, page: p, per_page: perPage } });
      const data = r.data || {};
      setItems(data.items || []);
      setTotal(data.meta?.total || 0);
      setPage(data.meta?.page || 1);
      setPerPage(data.meta?.per_page || perPage);
      setTotalPages(data.meta?.total_pages || 1);
    } catch (err) { setItems([]); setTotal(0); setTotalPages(1); }
  };

  const submit = async (e) => {
    e.preventDefault();
    // client validation
    setError("");
    if (!first.trim() || !last.trim()) {
      setError('First and Last name are required');
      return;
    }
    const payload = {
      first_name: first.trim(),
      last_name: last.trim(),
      contact: contact.trim(),
      dob: dob || undefined,
      sex: sex || undefined,
      address: address || undefined,
      clinical_id: clinicalId || undefined,
      allergies: allergies || undefined,
      history: history || undefined
    };
    try {
      await api.post('/patients/', payload);
      setMsg('Patient created');
      setFirst(''); setLast(''); setContact('');
      setDob(''); setSex(''); setAddress(''); setClinicalId(''); setAllergies(''); setHistory('');
      await fetchList(1);
    } catch (err) {
      setMsg('Error creating patient');
    }
    setTimeout(()=>setMsg(''),3000);
  };

  const onSelect = async (p) => {
    // fetch details for selected patient
    try {
      const r = await api.get(`/patients/${p._id}`);
      setSelected(r.data);
    } catch (err) {
      setError('Could not load patient details');
    }
  };

  const onDelete = async (id) => {
    if (!confirm('Delete this patient?')) return;
    try {
      await api.delete(`/patients/${id}`);
      setMsg('Patient deleted');
      await fetchList();
    } catch (err) {
      setError('Delete failed');
    }
    setTimeout(()=>setMsg(''),3000);
  };

  const onUpdate = async (id, data) => {
    // client validation
    if (!data.first_name || !data.last_name) { setError('First and Last name required'); return; }
    try {
      await api.put(`/patients/${id}`, data);
      setMsg('Patient updated');
      await fetchList();
      // refresh selected
      const r = await api.get(`/patients/${id}`);
      setSelected(r.data);
    } catch (err) {
      setError('Update failed');
    }
    setTimeout(()=>setMsg(''),3000);
    setTimeout(()=>setError(''),3000);
  };

  return (
    <div>
      <h2>Patients</h2>

      <section style={{marginBottom:20}}>
        <h3>Create Patient</h3>
        <form onSubmit={submit} style={{display:'flex',gap:8,alignItems:'center'}}>
          <input placeholder="First name" value={first} onChange={e=>setFirst(e.target.value)} />
          <input placeholder="Last name" value={last} onChange={e=>setLast(e.target.value)} />
          <input placeholder="Contact" value={contact} onChange={e=>setContact(e.target.value)} />
          <input type="date" placeholder="DOB" value={dob} onChange={e=>setDob(e.target.value)} />
          <select value={sex} onChange={e=>setSex(e.target.value)}>
            <option value="">Sex</option>
            <option value="Female">Female</option>
            <option value="Male">Male</option>
            <option value="Other">Other</option>
          </select>
          <input placeholder="Address" value={address} onChange={e=>setAddress(e.target.value)} />
          <input placeholder="Clinical ID" value={clinicalId} onChange={e=>setClinicalId(e.target.value)} />
          <input placeholder="Allergies" value={allergies} onChange={e=>setAllergies(e.target.value)} />
          <input placeholder="History" value={history} onChange={e=>setHistory(e.target.value)} />
          <button type="submit">Create</button>
          {msg && <span style={{marginLeft:10}}>{msg}</span>}
        </form>
      </section>

      <div style={{marginBottom:12, display:'flex', gap:8, alignItems:'center'}}>
        <input placeholder="Search by name" value={qStr} onChange={e=>setQStr(e.target.value)} />
        <button onClick={()=>{ setPage(1); fetchList(1); }}>Search</button>
        <label style={{marginLeft:12}}>Per page:
          <select value={perPage} onChange={e=>{ setPerPage(Number(e.target.value)); setPage(1); fetchList(1); }} style={{marginLeft:6}}>
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
          </select>
        </label>
        <div style={{marginLeft:'auto'}}>
          <strong>{total}</strong> total
        </div>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'2fr 1fr', gap:16}}>
        <div>
            <table style={{width:"100%",borderCollapse:"collapse"}}>
            <thead><tr><th>Name</th><th>Contact</th><th>Actions</th></tr></thead>
            <tbody>
              {items.map(p => (
                <tr key={p._id} style={{cursor:'pointer'}} onClick={()=>onSelect(p)}>
                  <td>{p.first_name} {p.last_name}</td>
                  <td>{p.contact}</td>
                  <td>
                    <button onClick={(e)=>{ e.stopPropagation(); navigator.clipboard.writeText(p._id); }}>Copy ID</button>
                    <button onClick={(e)=>{ e.stopPropagation(); onDelete(p._id); }} style={{marginLeft:8}}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div style={{marginTop:12, display:'flex', gap:8, alignItems:'center'}}>
            <button disabled={page<=1} onClick={()=>{ const np = Math.max(1, page-1); setPage(np); fetchList(np); }}>Prev</button>
            <span>Page {page} / {totalPages}</span>
            <button disabled={page>=totalPages} onClick={()=>{ const np = Math.min(totalPages, page+1); setPage(np); fetchList(np); }}>Next</button>
          </div>
        </div>

        <div style={{background:'#fff',padding:12,borderRadius:6,border:'1px solid #eee'}}>
          <h3>Details</h3>
          {selected ? (
            <PatientDetail patient={selected} onUpdate={onUpdate} onClose={()=>setSelected(null)} />
          ) : (
            <div>Select a patient row to view details</div>
          )}
        </div>
      </div>
    </div>
  );
}


function PatientDetail({patient, onUpdate, onClose}){
  const [first,setFirst] = useState(patient.first_name||'');
  const [last,setLast] = useState(patient.last_name||'');
  const [contact,setContact] = useState(patient.contact||'');
  const [dob,setDob] = useState(patient.dob||'');
  const [sex,setSex] = useState(patient.sex||'');
  const [address,setAddress] = useState(patient.address||'');
  const [clinicalId,setClinicalId] = useState(patient.clinical_id||'');
  const [allergies,setAllergies] = useState(patient.allergies||'');
  const [history,setHistory] = useState(patient.history||'');
  const [editing,setEditing] = useState(false);

  return (
    <div>
      {editing ? (
        <form onSubmit={async (e)=>{ e.preventDefault(); await onUpdate(patient._id, { first_name:first, last_name:last, contact, dob, sex, address, clinical_id: clinicalId, allergies, history }); setEditing(false); }}>
          <div style={{display:'flex',flexDirection:'column',gap:8}}>
            <input value={first} onChange={e=>setFirst(e.target.value)} />
            <input value={last} onChange={e=>setLast(e.target.value)} />
            <input value={contact} onChange={e=>setContact(e.target.value)} />
            <input type="date" value={dob} onChange={e=>setDob(e.target.value)} />
            <select value={sex} onChange={e=>setSex(e.target.value)}>
              <option value="">Sex</option>
              <option value="Female">Female</option>
              <option value="Male">Male</option>
              <option value="Other">Other</option>
            </select>
            <input value={address} onChange={e=>setAddress(e.target.value)} />
            <input value={clinicalId} onChange={e=>setClinicalId(e.target.value)} />
            <input value={allergies} onChange={e=>setAllergies(e.target.value)} />
            <input value={history} onChange={e=>setHistory(e.target.value)} />
            <div style={{display:'flex',gap:8}}>
              <button type="submit">Save</button>
              <button type="button" onClick={()=>setEditing(false)}>Cancel</button>
            </div>
          </div>
        </form>
      ) : (
        <div>
          <div><strong>Name:</strong> {patient.first_name} {patient.last_name}</div>
          <div><strong>Contact:</strong> {patient.contact}</div>
          <div><strong>DOB:</strong> {patient.dob}</div>
          <div><strong>Sex:</strong> {patient.sex}</div>
          <div><strong>Address:</strong> {patient.address}</div>
          <div><strong>Clinical ID:</strong> {patient.clinical_id}</div>
          <div><strong>Allergies:</strong> {patient.allergies}</div>
          <div><strong>History:</strong> {patient.history}</div>
          <div style={{marginTop:8}}>
            <button onClick={()=>setEditing(true)}>Edit</button>
            <button onClick={onClose} style={{marginLeft:8}}>Close</button>
          </div>
        </div>
      )}
    </div>
  )
}
