import './App.css';
import { Row, Col } from 'reactstrap';
import Cards from './components/cards';
function App() {
  return (
    <div className="App">
      <Row>
          <h1>Your deals</h1>
      </Row>
      <Row>
      <h2>In proccess</h2>
      </Row>
      <Col>
        <Cards type='in_process'/>
      </Col>
      <Row>
      <h2>Success</h2>
      <Col>
      <Cards type='success'/>
      </Col>
      </Row>
      <Row>
      <h2>Failure</h2>
      <Col>
      <Cards type='failure'/>
      </Col>
      </Row>
    </div>
  );
}

export default App;
