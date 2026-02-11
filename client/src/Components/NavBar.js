import { Link } from "react-router-dom"

export function NavBar() {
    return (
        <nav>
            <ul>
                <li><strong>Reviv Goli Soda</strong></li>
            </ul>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/UpdateInventory">Update </Link></li>
                <li><Link to="/MakeFlavor">Make </Link></li>
                <li><Link to="/ViewInventory">View</Link></li>
            </ul>
        </nav>
    )
}