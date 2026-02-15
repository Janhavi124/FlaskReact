import { Link, useNavigate, useLocation } from "react-router-dom"
import { useState, useEffect } from "react"

export function NavBar() {
    const [authenticated, setAuthenticated] = useState(false);
    const [user_name, setUsername] = useState("");
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        fetch("https://flaskreact-production-d646.up.railway.app/check_auth", {
            credentials: "include"
        })
        .then(res => res.json())
        .then(data => {
            setAuthenticated(data.authenticated);
            if (data.authenticated) setUsername(data.username);
        });
    }, [location]);

    const handleLogout = async () => {
        await fetch("https://flaskreact-production-d646.up.railway.app/logout", {
            method: "POST",
            credentials: "include"
        });
        setAuthenticated(false);
        navigate("/login");
    };

    return (
        <nav>
            <ul>
                <li><strong>Flavor Manager</strong></li>
            </ul>
            <ul>
                {authenticated ? (
                    <>
                        <li>Welcome, {user_name}!</li>
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/UpdateInventory">Update Inventory</Link></li>
                        <li><Link to="/MakeFlavor">Make Flavor</Link></li>
                        <li><button onClick={handleLogout}>Logout</button></li>
                    </>
                ) : (
                    <>
                        <li><Link to="/login">Login</Link></li>
                        <li><Link to="/register">Register</Link></li>
                    </>
                )}
            </ul>
        </nav>
    )
}