import Head from "next/head";
import Main from "../components/main/index";
import NavBar from "../components/navbar/index";
import images from "../public/images.json";

interface Props {
  id: number;
  latitude: number;
  longitude: number;
  note: string;
  time: string;
  url: string;
}

const data = images as Props[];

const Home = () => {
  // useState(() => {
  //   if (typeof window !== "undefined") {
  //   window.localStorage.setItem("data", JSON.stringify(data) as string);
  //   }
  // });
  return (
    <div className="bg-black">
      <Head>
        <title>Memor.i.eye</title>
      </Head>
      {/* <MapPage/> */}
      <NavBar />
      <Main data={data} />
    </div>
  );
};

export default Home;
