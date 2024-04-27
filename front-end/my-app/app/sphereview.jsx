
import React, { useEffect, useRef } from 'react';
import dynamic from 'next/dynamic';

// import { ReactPhotoSphereViewer } from 'react-photo-sphere-viewer';
const ReactPhotoSphereViewer = dynamic(
  () =>
    import('react-photo-sphere-viewer').then(
      (mod) => mod.ReactPhotoSphereViewer
    ),
  {
    ssr: false,
  }
);

export default function mapview() {  
  return (
    
      <ReactPhotoSphereViewer src="C:\Users\Belcher\Documents\SeniorDesignStarMap\front-end\my-app\images\starsky.jpg" height={'100vh'} width={"100%"}></ReactPhotoSphereViewer>
    
  );
}
