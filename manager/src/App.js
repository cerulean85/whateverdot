
import React from 'react'
import logo from './logo.svg';
import './App.css';


class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
        title: null
    }
  }

  componentDidMount() {

    fetch("http://localhost:3002/api")
        .then(res => res.json())
        .then(data => this.setState({title: data.title}))
  }

  render() {
    return (
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <div>
            {this.state.title}
            </div>
          </header>
        </div>
      );
  }


//   function App() {
//     return (
//       <div className="App">
//         <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <p>
//             Edit <code>src/App.js</code> and save to reload.
//           </p>
//           <a
//             className="App-link"
//             href="https://reactjs.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Learn React
//           </a>
//         </header>
//       </div>
//     );
//   }
}
export default App;
