
import React from 'react';

const mapFrame: React.FC<{imageUrl: string }> = ({ imageUrl }) => {

    return (

        <div style={{ display: 'flex', justifyContent: 'center',
            alignItems: 'center',
            width: '100vw', height: '100vh',
            border: '2px solid #000',
        }} >

            <img src={imageUrl} alt="DisplayedImage" style={{ maxWidth: '100%', maxHeight: '100%' }} />

        </div>

    );

};

export default mapFrame;
