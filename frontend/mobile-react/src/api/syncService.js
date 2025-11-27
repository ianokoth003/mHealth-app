import localforage from "localforage";
import api from "./axios";

localforage.config({ name: "healthease" });

export const saveLocalRecord = async (type, record) => {
  const key = `unsynced:${Date.now()}:${Math.random()}`;
  await localforage.setItem(key, { type, record, local_id: key });
  return key;
};

export const listUnsynced = async () => {
  const items = [];
  await localforage.iterate((value, k) => {
    if (k.startsWith("unsynced:")) items.push({ key: k, ...value });
  });
  return items;
};

export const clearLocalKey = (key) => localforage.removeItem(key);

export const uploadSync = async () => {
  const items = await listUnsynced();
  if (!items.length) return { uploaded: [] };
  const records = items.map(i => ({ type: i.type, data: i.record, local_id: i.key }));
  const resp = await api.post("/sync/upload", { records });
  // on success, remove local items matched by local_id
  const uploaded = resp.data.uploaded || [];
  for (const u of uploaded) {
    await clearLocalKey(u.local_id);
  }
  return resp.data;
};
