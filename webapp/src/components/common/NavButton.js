import React from 'react';
import PropTypes from 'prop-types';

const NavButton = ({ label, onClick }) => {
    return (
        <button className="mr-4" onClick={onClick}>
            {label}
        </button>
    );
};

NavButton.propTypes = {
    label: PropTypes.string.isRequired,
    onClick: PropTypes.func.isRequired,
};

export default NavButton;
