export default function BackArrow() {
  return (
    <div className="hover:bg-blue-800 active:bg-blue-900 bg-blue-600 opacity-80 h-fit w-fit p-4">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        style={{ fill: 'rgba(255, 255, 255, 1)' }}>
        <path d="M21 11H6.414l5.293-5.293-1.414-1.414L2.586 12l7.707 7.707 1.414-1.414L6.414 13H21z"></path>
      </svg>
    </div>
  )
}
