import React, { Component } from 'react';
import Webcam from 'react-webcam';
//https://github.com/mozmorris/react-webcam
class Camera extends Component {
  buttonClicked = () => {
    const imageSrc = this.webcam.getScreenshot();
    console.log(imageSrc);

    this.postData(imageSrc)
      .then(data => console.log(data));
  };

  postData = (data) => {
    return fetch('http://127.0.0.1:5000/infer', {
        method: 'POST',
        body: this.stripDataURL(data),
    })
    .then(response => response.json())
  }

  stripDataURL = (data) => {
      return data.replace(/^data:image\/\w+;base64,/, "");
  }

  setRef = (webcam) => {
    this.webcam = webcam;
  }

  render() {
    const buttonStyle = {
      fontSize: '20px',
      width: '200px',
    };
    return (
      <div>
        <Webcam 
          ref={this.setRef}
          screenshotFormat="image/jpeg"
        />
      
        <div>
          <button style={buttonStyle} onClick={this.buttonClicked} >
            Take Photo 
          </button>
        </div>

      </div>
    );
  }
}
export default Camera;
