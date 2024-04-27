import React from 'react';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
interface ImageBoxProps {
    imageUrl: string;
    altText: string;
}

const ImageBox: React.FC<ImageBoxProps> = ({ imageUrl, altText }) => {
    const boxStyle = {
        width: '600px', // Set the width of the box
        height: '580px', // Set the height of the box
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
        <TransformWrapper>
            <TransformComponent>
            <img src={imageUrl} alt={altText} style={imgStyle}/>
            </TransformComponent>
        </TransformWrapper>
    );
};

export default ImageBox;