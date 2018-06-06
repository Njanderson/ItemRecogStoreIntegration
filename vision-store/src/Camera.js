import React, { Component } from 'react';
import Webcam from 'react-webcam';
import Item from './Item';
//https://github.com/mozmorris/react-webcam
class Camera extends Component {

  constructor(props) {
    super(props);
    this.backend_url = 'http://applejack.cs.washington.edu:3000';
    this.state = {
      isLoading: false,
    };
  }

  awsClicked = () => {
    this.doRecog("/aws");
  };

  inferClicked = () => {
    this.doRecog("/infer");
  };

  doRecog = (route) => {
    this.setState({isLoading : true});
    const imageSrc = this.webcam.getScreenshot();
    //console.log(imageSrc);

    this.postData(route, imageSrc)
      .then(data => {
        console.log(data); 
        this.setState({itemData: data, isLoading: false});
      });
  };

  postData= (route, data) => {
    return fetch(this.backend_url + route, {
      method: 'POST',
      body: this.stripDataURL(data),
    })
      .then(response => {
        console.log(data);
        return response.json() 
      })
      .catch(err => {
        alert(err);
      })
  }

  stripDataURL = (data) => {
      return data.replace(/^data:image\/\w+;base64,/, "");
  }

  setRef = (webcam) => {
    this.webcam = webcam;
  }

  render() {
    const buttonDivStyle = {
      fontSize: '20px',
      color: "#ffffff",
      fontFamily: "HelveticaNeue-Light",
      paddingTop: "20px",
    };
    const buttonStyle = {
      width: '300px',
      height: '40px',
      fontSize: '30px',
      fontFamily: "HelveticaNeue-Light",
    };
    return (
      <div>
        <Webcam 
          ref={this.setRef}
          screenshotFormat="image/jpeg"
        />
      
        <div style={buttonDivStyle}>
          <button style={buttonStyle} onClick={this.vggClicked} >
            Take Photo: Infer with VGG
          </button>
        </div>
        <div style={buttonDivStyle}>
          <button style={buttonStyle} onClick={this.awsClicked} >
            Take Photo: Infer with AWS Rekognition
          </button>
        </div>
          <Item data={this.state}/>
      </div>
    );
  }
}
export default Camera;
