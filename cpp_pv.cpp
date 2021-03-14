#include<cstdio>
#include<cstdlib>
#include<string>


enum Operation{

   CREATE,
   EXTEND,
   REDUCE

};

int8_t run(const char* cmd){

try{
   if(system(NULL)) return system(cmd);
	  
}
catch(...){

	puts("Cannot execute....");

}
return 1;
}

void create_vg(std::string& vg_name,std::string& pvs){

	std::string cmd;
	cmd="vgcreate "+ vg_name +" "+pvs;
	run(cmd.c_str());
}


void create_pv(std::string& pv){
	std::string cmd ="pvcreate ";
	cmd+=pv;
	run(cmd.c_str());	
}

void manage_lv_part(std::string& vg_name,std::string& lv_name,std::string& size,Operation op,std::string format_type="ext4"){

	std::string cmd;
	std::string lv_path = " /dev/"+vg_name+"/"+lv_name;

	if(op == EXTEND){
	
		cmd ="lvextend -L +"+size+lv_path;
		run(cmd.c_str());
		cmd ="resize2fs "+lv_path;
		run(cmd.c_str());
		
	}
	else if(op == REDUCE){
		cmd = "umount "+lv_path;
		run(cmd.c_str());
		cmd = "e2fsck "+lv_path;
		run(cmd.c_str());
		cmd ="lvreduce -L -"+size+" "+lv_path;
		run(cmd.c_str());
		cmd ="resize2fs "+lv_path;
		run(cmd.c_str());
	}
	else if(op==CREATE){
	 	cmd ="lvcreate -L +"+size+" --name "+lv_name+" "+vg_name;
		run(cmd.c_str());
		cmd ="mkfs -t "+format_type+" "+lv_path;
		run(cmd.c_str());
	}
	else{
		puts("\n[ERR]: ENTER THE VALID OPERATION(CREATE | EXTEND | REDUCE )");
	}
}









int32_t main(int argc,char* argv[]){



std::string lv_name = "mylvm2";
std::string vg_name = "myvg1";
std::string pv_name = "/dev/xvdg";
std::string size="5M";
std::string format_type = "ext4";
//create_pv(pv_name);
manage_lv_part(vg_name,lv_name,size,REDUCE);

return 0;
}

