import React from 'react';
import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
interface ImageBoxProps {
    imageUrl: string;
    altText: string;
}

const ImageBox: React.FC<ImageBoxProps> = ({ imageUrl, altText }) => {;

    const imgStyle = {
        width: '70%',
        height: '70%',
        marginLeft:"auto",
        marginRight:"auto"
        // objectFit: 'cover' as 'cover' // Resize the image to cover the box, cropping it if necessary
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