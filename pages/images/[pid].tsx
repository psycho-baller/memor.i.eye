import { Container, Grid, GridItem, HStack } from "@chakra-ui/react";
import { useRouter } from "next/router";
import NavBar from "../../components/navbar";
import { ArrowBackIcon } from "@chakra-ui/icons";
import Image from "next/image";
import MoveTo from "../../components/main/moveTo";
import { useState } from "react";
import images from "../../public/images.json";

interface Props {
  id: number;
  latitude: number;
  longitude: number;
  note: string;
  time: string;
  url: string;
}

const ImageFocus = () => {
  const router = useRouter();

  const { pid } = router.query as { pid: string };
  let _data: Props[] = images;
    
  const id: number = parseInt(pid);
  for (let i = 0; i < _data.length; i++) {
    if (_data[i].id === id) {
      const prev = _data[i - 1] || _data[_data.length - 1];
      const next = _data[i + 1] || _data[0];
      // const { latitude, longitude, note, time, url } = _data[i];
      const date = new Date(_data[i].time);
      const time: string = date.toLocaleTimeString();
      const day: string = date.toDateString();
      return (
        <div className="bg-black">
          <NavBar />

          <Container maxW="95%" className="bg-black">
            <ArrowBackIcon
              boxSize={5}
              my={2.5}
              className="cursor-pointer"
              onClick={() => router.push("/")}
            />

            <Grid
              templateRows="repeat(3, 1fr)"
              templateColumns="repeat(9, 1fr)"
            >
              <GridItem rowSpan={2} colSpan={5}>
                <img
                  className="inside-image"
                  src={`${_data[i].url}`}
                  alt={_data[i].time}
                />
              </GridItem>
              <GridItem
                rowSpan={2}
                colSpan={4}
                className="text-white  text-center justify-content-center mt-12"
              >
                <h1 className="text-4xl">UWaterloo📍</h1>
                <h1 className="text-xl mb-4">200 University Ave W</h1>
                <Image src="/map.svg" height={140} width={140} />
              </GridItem>
              <GridItem
                className="text-white align-middle text-center justify-content-center"
                rowSpan={1}
                colSpan={5}
              >
                <h1 className="text-xs">{day}</h1>
                <h1 className="text-3xl font-bold">{time}</h1>
                <HStack justifyContent={"center"}>
                  <MoveTo data={prev} />
                  <MoveTo data={next} />
                </HStack>
              </GridItem>
            </Grid>
          </Container>
        </div>
      );
    }
  }
};

export default ImageFocus;
