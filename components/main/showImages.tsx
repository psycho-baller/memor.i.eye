import { Heading } from "@chakra-ui/react";
import { motion } from "framer-motion";
import Link from "next/link";

interface Props {
  id: number;
  latitude: number;
  longitude: number;
  note: string;
  time: string;
  url: string;
}

export default function ShowImages({
  dates, data, show
}: {
  dates: { [key: string]: Props[] }, data: Props[], show: string;
}) {
  return (
    <div >
        {Object.keys(dates).sort().map((date) => {
            return (
              <div className="mt-2"  key={date}>
                <Heading size="md">{date}</Heading>
                <div className="hstack">
                  {dates[date].map((image) => {
                    return (
                      <Link
                        key={image.id}
                        href={{
                          pathname: `/images/${image.id}`,
                        }}
                      >
                        <motion.img
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.95 }}
                          src={`images/${image.url}`}
                          alt={image.time}
                          className="image"
                        />
                      </Link>
                    );
                  })}
                </div>
              </div>
            );
        })}
        
    </div>
  );
}
