import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5000/api";

// Test connection to backend
async function testConnection() {
  try {
    const response = await axios.get("http://127.0.0.1:5000/");
    console.log("✅ Admin App - Backend Connected!");
    console.log("Response:", response.data);
    return true;
  } catch (error) {
    console.error("❌ Admin App - Connection Failed!");
    console.error("Error:", error.message);
    return false;
  }
}

testConnection();
