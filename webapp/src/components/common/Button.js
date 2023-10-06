const Button = ({ label, onClick, className }) => {
    return (
        <button onClick={onClick} className={`p-3 ${className}`}>
            {label}
        </button>
    );
};

export default Button;
