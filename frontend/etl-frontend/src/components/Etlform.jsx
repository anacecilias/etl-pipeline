import { useState } from "react";
import "./Etlform.css";

export default function AuthForm() {
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [password, setPassword] = useState("");

  const getPasswordStrength = (pwd) => {
    if (!pwd || pwd.includes(" ")) return 0;
    
    const hasMinLength = pwd.length >= 6;
    const hasUpperLower = /[A-Z]/.test(pwd) && /[a-z]/.test(pwd);
    const hasNumber = /\d/.test(pwd);
    const hasSpecial = /[^A-Za-z0-9]/.test(pwd);
    
    if (hasMinLength && hasUpperLower && hasNumber && hasSpecial) return 3;
    if ([hasMinLength, hasUpperLower, hasNumber, hasSpecial].filter(Boolean).length >= 3) return 2;
    if ([hasMinLength, hasUpperLower, hasNumber, hasSpecial].filter(Boolean).length >= 1) return 1;
    
    return 0;
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value.replace(/\s/g, ""));
  };

  const strengthLevel = getPasswordStrength(password);
  const strengthLabels = ["Fraca", "Média", "Forte"];

  return (
    <div className="box">
      <div className="container">
        <div className="top-header">
          <span>{isLogin ? "Não tem conta?" : "Já tem conta?"}</span>
          <header>{isLogin ? "Login" : "Cadastro"}</header>
        </div>

        <div className="input-field">
          <i className="bx bx-envelope"></i>
          <input type="email" placeholder="E-mail" />
        </div>

        {!isLogin && (
          <div className="input-field">
            <i className="bx bx-user"></i>
            <input type="text" placeholder="Username" />
          </div>
        )}

        {/* este cao desse olho pra mostrar e ocultar senha */}
        
        <div className="input-field">
          <i className="bx bx-lock-alt"></i>
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Senha (mín. 6 caracteres)"
            value={password}
            onChange={handlePasswordChange}/>
          <button
            type="button"
            className="eye-btn"
            onClick={() => setShowPassword(!showPassword)}>
            <i className={`bx ${showPassword ? "bx-hide" : "bx-show"}`}></i>
          </button>
        </div>

        {!isLogin && password && strengthLevel > 0 && (
          <div className={`strength-bar level-${strengthLevel}`}>
            <div className="bar-fill"></div>
            <span className="strength-text">{strengthLabels[strengthLevel - 1]}</span>
          </div>
        )}

        <button className="submit-btn">
          {isLogin ? "Entrar" : "Criar conta"}
        </button>

        <div className="divider">
          <span>ou entre com</span>
        </div>

        <div className="social-btns">
          <button className="social-btn">
            <i className="bx bxl-google"></i>
          </button>
          <button className="social-btn">
            <i className="bx bxl-github"></i>
          </button>
        </div>

        <div className="footer-link">
          <button className="toggle-link" onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? "Criar conta" : "Voltar para login"}
          </button>
        </div>
      </div>
    </div>
  );
}