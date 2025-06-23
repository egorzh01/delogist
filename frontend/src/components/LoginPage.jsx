import { useState } from "react";
import {
  Box, Button, Card, TextField, Typography, Alert
} from "@mui/material";
import axios from "axios";

export default function LoginPage({ setToken }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin() {
    if (!username || !password) {
      setError("Введите логин и пароль");
      return;
    }
    try {
      const res = await axios.post("api/auth/", {
        username,
        password,
      });

      localStorage.setItem("authToken", res.data.token);
      setToken(res.data.token);
    } catch {
      setError("Неверный логин или пароль");
    }
  }

  return (
    <Box minHeight="100vh" display="flex" alignItems="center" justifyContent="center" >
      <Card sx={{ p: 4, minWidth: 320 }}>
        <Typography variant="h6" mb={2}>Вход</Typography>
        <TextField
          fullWidth
          label="Логин"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          margin="normal"
        />
        <TextField
          fullWidth
          type="password"
          label="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          margin="normal"
        />
        {error && <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>}
        <Button
          variant="contained"
          fullWidth
          onClick={handleLogin}
          sx={{ mt: 2 }}
        >
          Войти
        </Button>
      </Card>
    </Box>
  );
}
