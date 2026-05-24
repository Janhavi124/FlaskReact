/**export function HomePage() {
    return (
        <>
        <h1>Hello!</h1>
    </>
    )
} **/ 

/** Minor change to make a commit - This version as of 5/24/2026 has basic functionality and is hosted on render, supabase and vercel */
export function HomePage() {
  const user_name = localStorage.getItem("user_name");

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Hello, {user_name}! 👋</h1>
    </div>
  );
}
