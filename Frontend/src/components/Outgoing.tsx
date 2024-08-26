import Image from 'next/image';
import user from '/public/user.svg'

interface Props{
    children?: React.ReactNode;
    itemKey?: number;
}

const Outgoing = ({children, itemKey}:Props) => {
    return (
        <div key={itemKey} className="flex justify-end mb-4 cursor-pointer">
            <div className="flex max-w-96 bg-indigo-500 text-white rounded-lg p-3 gap-3">
                <p>{children}</p>
            </div>
            <div className="w-9 h-9 rounded-full flex items-center justify-center ml-2">
                <Image src={user} alt="My Avatar" className="w-8 h-8 rounded-full"/>
            </div>
        </div>
    )
}

export default Outgoing;