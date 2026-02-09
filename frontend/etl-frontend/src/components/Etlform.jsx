import "./Etlform.css";

export default function Etlform() {
  return (
    <div className="login-box">
        <h2>Seja bem-vindo</h2>
        <form action="">
            <div className="input-box">
                <input type="text" required/>
                <label for="username">Username</label>
                <span></span>
            </div>
            <div className="input-box">
                <input type="password" required/>
                <label for="password">Senha</label>
                <span></span>
            </div>
            <div className="options">
                <label for=""><input type="checkbox"/> Lembre-se de mim</label>
                <a href="#">Esqueceu sua senha?</a>
            </div>
            <button>Entrar</button>
            <div className="register">Novo por aqui?
                <a href="#">Registrar-se</a>
            </div>
        </form>
    </div>
  );
}
