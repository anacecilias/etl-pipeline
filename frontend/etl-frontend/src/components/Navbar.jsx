import './Navbar.css'

export default function Navbar() {
  return (
    <nav className="navbar">
      <h2>ETL Studio</h2>
      <div className="links">
        <a href="#">Home</a>
        <a href="#">Configuração</a>
        <a href="#">Executar</a>
      </div>
    </nav>
  )
}
