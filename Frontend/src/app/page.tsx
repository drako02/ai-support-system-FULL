import Link from "next/link";

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-5xl font-bold mb-4">Welcome to Home </h1>
      <Link href="/login" className="bg-blue-500 text-white p-2 rounded">
        Go to Login
      </Link>
    </div>
  )
}  

export default Home;