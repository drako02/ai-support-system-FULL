import Image from 'next/image';
import support from '/public/support.svg'

interface Props {
    children?: React.ReactNode;
    itemKey?: number;
}

const Incoming = ({ children, itemKey }: Props) => {
    return (
        <div key={itemKey} className="flex mb-4 cursor-pointer">
            <div className="w-9 h-9 rounded-full flex items-center justify-center mr-2">
                <Image src={support} alt="User Avatar" className="w-8 h-8 rounded-full"/>
            </div>
            <div className="flex max-w-96 bg-white rounded-lg p-3 gap-3">
                <p className="text-gray-700">{ children}</p>
            </div>
        </div>
    )
}
export default Incoming;