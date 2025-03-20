import { View, Text, TextInput, TouchableOpacity } from "react-native";
import { useState } from "react";
import { useRouter } from "expo-router";
import tw from "tailwind-react-native-classnames";
import { login } from "../api/loginApi";  

export default function LoginScreen() {
  const router = useRouter();

  // Estados para los campos del formulario
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mensaje, setMensaje] = useState("");


  const handleLogin = async () => {
    try {
      
      const data = await login(email, password);

      router.push("/main");
    } catch (error) {
      setMensaje(error.response?.data?.error || "Error de conexión");
    }
  };

  return (
    <View style={tw`flex-1 justify-center px-6 py-12 bg-white`}>
      {/* Logo */}
      <View style={tw`flex-1 justify-center items-center`}>
        <Text style={tw`text-4xl font-bold text-gray-900`}>POS FC</Text>
      </View>

      <View style={tw`items-center`}>
        <Text style={tw`text-2xl font-bold text-gray-900`}>Iniciar Sesión</Text>
      </View>

      {/* Formulario */}
      <View style={tw`mt-8 w-1/2 mx-auto`}>
        {/* Email */}
        <View style={tw`mb-4`}>
          <Text style={tw`text-gray-900 font-semibold mb-1`}>Correo Electrónico</Text>
          <TextInput
            placeholder="tuemail@ejemplo.com"
            style={tw`border border-gray-300 rounded-md px-3 py-2 text-gray-900`}
            value={email}
            onChangeText={setEmail} 
          />
        </View>

        <View style={tw`mb-4`}>
          <Text style={tw`text-gray-900 font-semibold mb-1`}>Contraseña</Text>
          <TextInput
            placeholder="••••••••"
            secureTextEntry
            style={tw`border border-gray-300 rounded-md px-3 py-2 text-gray-900`}
            value={password}
            onChangeText={setPassword} 
          />
        </View>

        {/* Botón de Iniciar Sesión */}
        <TouchableOpacity
          onPress={handleLogin}
          style={tw`bg-indigo-600 py-3 rounded-md mt-4`}
        >
          <Text style={tw`text-white text-center font-semibold`}>Iniciar Sesión</Text>
        </TouchableOpacity>

        
        {mensaje ? <Text style={tw`text-center text-red-500 mt-4`}>{mensaje}</Text> : null}

        
        <Text style={tw`text-center text-gray-500 mt-6`}>
          ¿No tienes cuenta?{" "}
          <Text style={tw`text-indigo-600 font-semibold`} onPress={() => router.push("/register")}>
            Regístrate aquí
          </Text>
        </Text>
      </View>
    </View>
  );
}
