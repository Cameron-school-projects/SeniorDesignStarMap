import React from 'react';

interface ImageBoxProps {
    imageUrl: string;
    altText: string;
}

const ImageBox: React.FC<ImageBoxProps> = ({ imageUrl, altText }) => {
    const boxStyle = {
        width: '800px', // Set the width of the box
        height: '580px', // Set the height of the box
        border: '2px solid black', // Optional: adds a border around the image box
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        overflow: 'hidden' // Ensures the image does not exceed the box
    };

    const imgStyle = {
        width: '100%',
        height: '100%',
        objectFit: 'cover' as 'cover' // Resize the image to cover the box, cropping it if necessary
    };
    
    return (
        <div className="image-box" style={boxStyle}>
            <img src={imageUrl} alt={altText} style={imgStyle}/>
        </div>
    );
};

export default ImageBox;