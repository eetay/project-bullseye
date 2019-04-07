import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor (props) {
    super()
    this.imageRef = React.createRef();
  }

  componentDidMount(_props) {
    var self = this
    let a = setInterval(function () {
      let offsetTop = Math.floor(Math.random() * 10) * 10;
      let offsetLeft = Math.floor(Math.random() * 10) * 10;
      self.moveTarget({image: self.imageRef.current, offsetTop, offsetLeft})
    }, 500)
    console.log(a)
  }

  moveTarget = ({image, offsetTop, offsetLeft}) => {
    let img = image
    console.log('moveTarget')
    img.style.position = 'absolute';
    img.style.top = offsetTop + 'px';
    img.style.left = offsetLeft + 'px';
    img.style.display = "block";
  }

  render() {
    //let ctx = canvas.getContext('2d');
    return (
      <div className="App">
        <header className="App-header" height="400px" width="400px">
          <img ref={this.imageRef} src={logo} className="App-logo" alt="logo" /> 
        </header>
      </div>
    );
  }
}

export default App;
