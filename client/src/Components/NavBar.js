import { Link, useNavigate, useLocation } from "react-router-dom"
import { useState, useEffect } from "react"

export function NavBar() {
    const [authenticated, setAuthenticated] = useState(false);
    const [user_name, setUsername] = useState("");
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const token = localStorage.getItem('token');
        
        if (!token) {
            setAuthenticated(false);
            return;
        }

        fetch("https://flaskreact-production-d646.up.railway.app/check_auth", {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.authenticated) {
                setAuthenticated(true);
                setUsername(data.user_name);
            } else {
                setAuthenticated(false);
                localStorage.removeItem('token');
                localStorage.removeItem('user_name');
            }
        })
        .catch(() => {
            setAuthenticated(false);
        });
    }, [location]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user_name');
        setAuthenticated(false);
        navigate("/login");
    };

    return (
        <nav>
            <ul>
                <li><strong>Reviv</strong></li>
            </ul>
            <ul>
                {authenticated ? (
                    <>
                        <li>Welcome, {user_name}!</li>
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/UpdateInventory">Update </Link></li>
                        <li><Link to="/MakeFlavor">Make </Link></li>
                        <li><Link to="/ViewInventory">View</Link></li>
                        <li><Link to="/ViewBatches">Batches</Link></li>
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