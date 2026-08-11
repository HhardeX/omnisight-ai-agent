function Logo() {
  return (
    <div className="omnisight-logo">
      <div className="logo-icon">
        <svg
          width="38"
          height="38"
          viewBox="0 0 48 48"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M4 24C9 14 16 9 24 9C32 9 39 14 44 24C39 34 32 39 24 39C16 39 9 34 4 24Z"
            stroke="currentColor"
            strokeWidth="3"
          />

          <circle cx="24" cy="24" r="8" fill="currentColor" />

          <circle cx="24" cy="24" r="3" fill="white" />

          <path
            d="M35 7L36.5 11.5L41 13L36.5 14.5L35 19L33.5 14.5L29 13L33.5 11.5L35 7Z"
            fill="currentColor"
          />
        </svg>
      </div>

      <div className="logo-text">
        <span className="logo-omni">Omni</span>
        <span className="logo-sight">Sight</span>
      </div>
    </div>
  );
}

export default Logo;
