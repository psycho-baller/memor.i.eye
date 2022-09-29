import {
  Flex,
  Input,
  InputGroup,
  InputLeftElement,
  Grid,
  GridItem,
  Icon,
  Text
} from "@chakra-ui/react";
import { SearchIcon } from "@chakra-ui/icons";
import { CgProfile } from "react-icons/cg";
import router from "next/router";
import { SetStateAction, useState } from "react";
import { motion } from "framer-motion";
import { logoI } from "../../animations/logo";

export default function NavBar() {

    const [data, setData] = useState("");
    const [value, setValue] = useState("");
    const handleChange = (event: { target: { value: SetStateAction<string>; }; }) => setValue(event.target.value);

    const fetchData = async () => {
        const res = await fetch(`http://20.25.130.61/search?q=${value}`);
        const newData = await res.json();      

      return setData(newData.results);
    };

//     async function handleSearch(e: React.KeyboardEvent<HTMLInputElement>) {
//         if (e.key === "Enter") {
// const res = await fetch(`http://20.25.130.61/search?q=${value}`);
// const newData = await res.json();
// console.log(res);

// return setData(newData.results);        }
//     }
    function handleSubmit(e: any) {
        e.preventDefault();
        fetchData();
    }

  return (
    <Grid
      alignItems="center"
      className="pt-2.5 pb-3 px-1 bg-zinc-900 justify-center"
      templateColumns="repeat(3, 1fr)"
    >
      <GridItem pl="2" className="justify-center">
        <Text
          className="cursor-pointer"
          onClick={() => router.push("/")}
          fontWeight={700}
          size="27px"
        >
          memor.
          <motion.span
            initial="hidden"
            animate="visible"
            whileHover="hover"
            variants={logoI}
            className="logo-name inline-block"
          >
            i
          </motion.span>
          .eye
        </Text>
      </GridItem>

      <InputGroup>
        <InputLeftElement
          className="cursor-pointer"
          //   onClick={handleSubmit}
        >
          <SearchIcon color="gray.300" />
        </InputLeftElement>
        <Input
          placeholder="Search Memories"
          value={value}
          onChange={handleChange}
        />
      </InputGroup>

      <Flex className="justify-end">
        <Icon as={CgProfile} className="mx-4 my-2 cursor-pointer" w={6} h={6} />
      </Flex>
    </Grid>
  );
}
