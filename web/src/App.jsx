import { useState } from 'react'
import './App.css'
import DeliveryReport from './components/DeliveryReport'
import LoginPage from './components/LoginPage';

function App() {
  const [token, setToken] = useState(localStorage.getItem("authToken"));
  if (!token) {
    return <LoginPage setToken={setToken} />;
  }
  return (
    <DeliveryReport />
  )
}

export default App
