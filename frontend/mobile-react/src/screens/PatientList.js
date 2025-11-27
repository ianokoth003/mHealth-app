import React, {useEffect, useState} from "react";
import api from "../api/axios";
import { listUnsynced, clearLocalKey } from "../api/syncService";

function PatientDetail({patient, onClose, onSave, onDelete}){
  const [editing, setEditing] = useState(false);
  const [first, setFirst] = useState(patient.first_name || "");
  const [last, setLast] = useState(patient.last_name || "");
  const [contact, setContact] = useState(patient.contact || "");

  useEffect(()=>{
    setFirst(patient.first_name || "");
    setLast(patient.last_name || "");
    setContact(patient.contact || "");
  }, [patient]);

  const save = async ()=>{
    await onSave(patient._id, { first_name: first, last_name: last, contact });
    setEditing(false);
  };

  return (
    <div>
      {editing ? (
        <div style={{display:'flex',flexDirection:'column',gap:8}}>
          <input value={first} onChange={e=>setFirst(e.target.value)} />
          <input value={last} onChange={e=>setLast(e.target.value)} />
          <input value={contact} onChange={e=>setContact(e.target.value)} />
          <div style={{display:'flex',gap:8}}>
            <button onClick={save}>Save</button>
            <button onClick={()=>setEditing(false)}>Cancel</button>
          </div>
        </div>
      ) : (
        <div>
          <div><strong>Name:</strong> {patient.first_name} {patient.last_name}</div>
          <div><strong>Contact:</strong> {patient.contact}</div>
          <div style={{marginTop:8}}>
            <button onClick={()=>setEditing(true)}>Edit</button>
            <button onClick={()=>onDelete(patient._id)} style={{marginLeft:8}}>Delete</button>
            <button onClick={onClose} style={{marginLeft:8}}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default function PatientList(){
  const [items,setItems] = useState([]);
  const [q,setQ] = useState("");
  const [page,setPage] = useState(1);
  const [perPage,setPerPage] = useState(10);
  const [totalPages,setTotalPages] = useState(1);
  const [message,setMessage] = useState("");
  const [selected,setSelected] = useState(null);

  useEffect(() => {
    fetchList();
  }, [page, perPage]);

  const fetchList = async ()=>{
    try {
      const r = await api.get("/patients", { params: { q: q || undefined, page, per_page: perPage } });
      const data = r.data || {};
      let serverItems = data.items || [];
      // load local unsynced records and append them to list with a marker
      const local = await listUnsynced();
      const localPatients = local.filter(i => i.type === 'patient').map(i => ({ _id: i.local_id, ...i.record, _local: true, _local_key: i.key }));
      setItems([...localPatients, ...serverItems]);
      setTotalPages(data.meta?.total_pages || 1);
    } catch (err) {
      setItems([]);
    }
  };

  const showMsg = (m)=>{ setMessage(m); setTimeout(()=>setMessage(''),3000); };

  const onSelect = async (p)=>{
    // if local record, open detail with local flag
    if (p._local){
      setSelected(p);
      return;
    }
    try {
      const r = await api.get(`/patients/${p._id}`);
      setSelected(r.data);
    } catch (err) {
      showMsg('Failed to load details');
    }
  };

  const onDelete = async (id)=>{
    // handle local vs server
    const item = items.find(it => it._id === id);
    if (!item) return;
    if (item._local){
      // remove local key
      await clearLocalKey(item._local_key);
      showMsg('Local patient deleted');
      fetchList();
      setSelected(null);
      return;
    }

    if (!confirm('Delete this patient?')) return;
    try {
      await api.delete(`/patients/${id}`);
      showMsg('Patient deleted');
      fetchList();
      setSelected(null);
    } catch (err) {
      showMsg('Delete failed');
    }
  };

  const onSave = async (id, data)=>{
    // handle local vs server save
    const item = items.find(it => it._id === id);
    if (item && item._local){
      // for local, update localforage item
      // simple approach: remove old local and save new local record
      await clearLocalKey(item._local_key);
      await listUnsynced();
      // save updated local record
      // reuse saveLocalRecord to persist
      const { saveLocalRecord } = await import('../api/syncService');
      await saveLocalRecord('patient', data);
      showMsg('Local patient updated');
      fetchList();
      return;
    }

    try {
      await api.put(`/patients/${id}`, data);
      showMsg('Patient updated');
      fetchList();
    } catch (err) {
      showMsg('Update failed');
    }
  };

  return (
    <div>
      <div style={{display:"flex", alignItems:'center', gap:8}}>
        <input placeholder="Search" value={q} onChange={e=>setQ(e.target.value)} />
        <button onClick={()=>{ setPage(1); fetchList(); }}>Search</button>
        <label style={{marginLeft:12}}>Per page:
          <select value={perPage} onChange={e=>{ setPerPage(Number(e.target.value)); setPage(1); }} style={{marginLeft:6}}>
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={20}>20</option>
          </select>
        </label>
      </div>
      <ul>
        {items.map(p => (
          <li key={p._id} style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:6,borderBottom:'1px solid #eee',cursor:'pointer'}} onClick={()=>onSelect(p)}>
            <div>
              <div><strong>{p.first_name} {p.last_name}</strong> {p._local && <span style={{color:'#b85'}}>• offline</span>}</div>
              <div style={{fontSize:12,color:'#666'}}>{p.contact}</div>
            </div>
            <div>
              <button onClick={(e)=>{ e.stopPropagation(); navigator.clipboard.writeText(p._id); }}>Copy ID</button>
              <button onClick={(e)=>{ e.stopPropagation(); onDelete(p._id); }} style={{marginLeft:8}}>Delete</button>
            </div>
          </li>
        ))}
      </ul>

      <div style={{display:'flex', gap:8, alignItems:'center'}}>
        <button disabled={page<=1} onClick={()=>{ setPage(Math.max(1, page-1)); }}>Prev</button>
        <span>Page {page} / {totalPages}</span>
        <button disabled={page>=totalPages} onClick={()=>{ setPage(Math.min(totalPages, page+1)); }}>Next</button>
        <button style={{marginLeft:12}} onClick={()=>{ setPage(1); fetchList(); }}>Refresh</button>
      </div>
      {message && <div style={{position:'fixed',right:20,bottom:20,background:'#222',color:'#fff',padding:'8px 12px',borderRadius:6}}>{message}</div>}

      {selected && <div style={{position:'fixed',left:20,top:60,right:20,bottom:20,background:'rgba(0,0,0,0.4)',display:'flex',alignItems:'center',justifyContent:'center'}}>
        <div style={{background:'#fff',padding:16,borderRadius:8,width:420,maxHeight:'80%',overflow:'auto'}}>
          <PatientDetail patient={selected} onClose={()=>setSelected(null)} onSave={onSave} onDelete={onDelete} />
        </div>
      </div>}
    </div>
  );
}
