import { Heading } from "@chakra-ui/react";
import { motion } from "framer-motion";
import Link from "next/link";
import router from "next/router";

interface Props {
  id: number;
  latitude: number;
  longitude: number;
  note: string;
  time: string;
  url: string;
}
export default function ShowImages({
  data,
}: {
  data: Props;
}) {
  return (
    
      <motion.img
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        src={data.url}
        alt={data.time}
        className="image"
        height={100}
        width={100}
        onClick={() => router.push(`/images/${data.id}`)}
      />
  );
}

// Language: typescript
// Path: frontend\components\main\showImages.tsx
// Compare this snippet from frontend\components\main\moveTo.tsx:
// import { Heading } from "@chakra-ui/react";
// import { motion } from "framer-motion";
// import Link from "next/link";
//
// interface Props {
//   id: number;
//   latitude: number;
//   longitude: number;
//   note: string;
//   time: string;
//   url: string;
// }
//
// export default function ShowImages({
//   dates, data
// }: {
//   dates: { [key: string]: Props[] }, data: Props[];
// }) {
//   return (
//     <div >
//         {Object.keys(dates).sort().map((date) => {
//             return (
//               <div className="mt-4"  key={date}>
//                 <Heading size="md">{date}</Heading>
//                 <div className="hstack">
//                   {dates[date].map((image) => {
//                     return (
//                       <Link
//                         key={image.id}
//                         href={{
//                           pathname: `/images/${image.id}`,
//                           query: { data: JSON.stringify(data) },
//                         }}
//                       >
//                         <motion.img
//                           whileHover={{ scale: 1.1
