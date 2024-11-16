import {Outlet, Route, Routes} from "react-router-dom";
import NoMatch from "./pages/NoMatch";
import Home from "./pages/Home";
import Landing from "./pages/Landing";
import Header from "./components/header/Header";
import {Container} from "@mantine/core";


function Layout() {
  return (
      <div className="layout">
        <Header/>
        <Container py={10}>
          <Outlet/>
        </Container>
      </div>
  );
}

function App() {
  return (
      <div className="App">
        <Routes>
          <Route path="/" element={<Layout/>}>
            <Route index element={<Landing/>}/>
            <Route path="app" element={<Home/>}/>
            <Route path="*" element={<NoMatch/>}/>
          </Route>
        </Routes>
      </div>
  );
}

export default App;
