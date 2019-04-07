import React, { Component } from 'react';
import logo from './bullseye.png'
import './App.css';



class App extends Component {
  constructor (props) {
    super()
    this.imageRef = React.createRef();
    this.x=this.y=1
  }

  componentDidMount(_props) {
    var self = this
    self.exampleSocket = new WebSocket("ws://localhost:9999");
    self.exampleSocket.onmessage = function (event) {
      console.log('got event', event.data);
      let {offsetTop, offsetLeft} = JSON.parse(event.data)
      self.moveTarget({
        image: self.imageRef.current, 
        offsetTop, 
        offsetLeft
      })
    }
    self.exampleSocket.onopen = function (event) {
      console.log('connected', event);
      if (event.type === 'open') {
        self.exampleSocket.connected = true 
      }
    };
    /*
    let a = setInterval(function () {
      let offsetTop = self.y++;
      let offsetLeft = self.x++;
      self.moveTarget({image: self.imageRef.current, offsetTop, offsetLeft})
    }, 500)
    console.log(a)
    */
  }

  moveTarget = ({image, offsetTop, offsetLeft}) => {
    let img = image
    console.log('moveTarget')
    img.style.position = 'absolute';
    img.style.top = offsetTop + 'px';
    img.style.left = offsetLeft + 'px';
    img.style.display = "block";
    if (this.exampleSocket.connected) this.exampleSocket.send(JSON.stringify({offsetTop, offsetLeft}));
  }

  render() {
    return (
      <div className="App">
        <header className="App-header" height="100%" width="100%">
          <img ref={this.imageRef} src={logo} className="App-logo" alt="logo"/> 
        </header>
      </div>
    );
  }
}

export default App;
