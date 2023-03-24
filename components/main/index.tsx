import {
  Container,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";

import { isThisMonth, isThisYear, isToday } from "../../utils/checkToday";
import ShowImages from "./showImages";

interface Props {
  id: number;
  latitude: number;
  longitude: number;
  note: string;
  time: string;
  url: string;
}

function Main(props: any) {
  const data = props.data as Props[];
  const datesD = {} as { [key: string]: Props[] };
  const datesM = {} as { [key: string]: Props[] };
  const datesY = {} as { [key: string]: Props[] };
  data.map((image) => {
    const date = new Date(image.time);
    if (isToday(date)) {
      datesD["Today"] = datesD["Today"] || [];
      datesD["Today"].push(image);
    } else {
      const day = date.toDateString();
      if (datesD[day] === undefined) {
        datesD[day] = [];
      }
      datesD[day].push(image);
    }

    if (isThisMonth(date)) {
      datesM["This Month"] = datesM["This Month"] || [];
      datesM["This Month"].push(image);
    } else {
      const month = date.getMonth() + 1;
      if (datesM[month] === undefined) {
        datesM[month] = [];
      }
      datesM[month].push(image);
    }
    if (isThisYear(date)) {
      datesY["This Year"] = datesY["This Year"] || [];
      datesY["This Year"].push(image);
    } else {
      const year = date.getFullYear();
      if (datesY[year] === undefined) {
        datesY[year] = [];
      }
      datesY[year].push(image);
    }
  });

  return (
    <Container maxW="95%">
      <Tabs size="sm" isFitted variant="enclosed" colorScheme="white">
        <TabList mt="0.5em">
          <Tab>Days</Tab>
          <Tab>Months</Tab>
          <Tab>Years</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <ShowImages show={"days"} dates={datesD} data={data} />
          </TabPanel>
          <TabPanel>
            <ShowImages show={"months"} dates={datesM} data={data} />
          </TabPanel>
          <TabPanel>
            <ShowImages show={"years"} dates={datesY} data={data} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Container>
  );
}

export default Main;
