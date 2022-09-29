import { motion } from "framer-motion";

const variants = {
  open: {
    y: 0,
    opacity: 1,
    transition: {
      y: { stiffness: 1000, velocity: -100 },
    },
  },
  closed: {
    y: 50,
    opacity: 0,
    transition: {
      y: { stiffness: 1000 },
    },
  },
};
interface Props {
    id: number;
    text: string;
}
const colors = ["#fef6e4", "#f582ae", "#8bd3dd", "#b8c1ec", "#ff8906"];

export const MenuItem = ({ id, text }: Props) => {
  const style = { border: `3px solid ${colors[id]}` };
  return (
    <motion.li
      variants={variants}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      className="flex items-center justify-center w-12 h-12 mb-6 text-2xl text-white bg-black rounded-full cursor-pointer"
    >

      <div className="text-placeholder">
        <span className="text">{text}</span>
      </div>
    </motion.li>
  );
};
