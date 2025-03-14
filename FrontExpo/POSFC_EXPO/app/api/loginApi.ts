import axios from "axios";

// URL de la API
const API_URL = "http://127.0.0.1:8000/login_usuario";

export const login = async (email: string, password: string) => {
  try {
    const response = await axios.post(
      API_URL,
      {
        usuario: email,  // Nombre de usuario
        password: password,  // Contraseña
      },
      {
        withCredentials: true,  // Importante para que las cookies HTTPOnly se envíen automáticamente
      }
    );
    
    return response.data;  // El backend ya almacena el token en la cookie
  } catch (error) {
    throw error;
  }
};
